// Developer-only live MapLibre smoke test. Not shipped with Syntyr CSS.
// SYNTYR_VENDOR_NODE_MODULES=/path/to/app/node_modules node tests/geo_maplibre_browser.mjs
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import { existsSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { createServer } from "node:http";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const vendor = process.env.SYNTYR_VENDOR_NODE_MODULES;
if (!vendor) throw new Error("Set SYNTYR_VENDOR_NODE_MODULES to an app node_modules path");
const files = {
  pw: path.join(vendor, "playwright", "index.mjs"),
  esbuild: path.join(vendor, "esbuild", "lib", "main.js"),
  css: path.join(vendor, "maplibre-gl", "dist", "maplibre-gl.css"),
  worker: path.join(vendor, "maplibre-gl", "dist", "maplibre-gl-worker.mjs"),
};
for (const f of Object.values(files)) if (!existsSync(f)) throw new Error("Missing dev-only file: " + f);
const { chromium } = await import(pathToFileURL(files.pw).href);
const { build } = await import(pathToFileURL(files.esbuild).href);
const compiled = await build({
  stdin: { contents: 'import * as maplibregl from "maplibre-gl"; window.maplibregl = maplibregl;', resolveDir: vendor, sourcefile:"syntyr-geo-maplibre-entry.js" },
  platform: "browser", format: "iife", bundle: true, write: false, target: "es2022",
});
const script = compiled.outputFiles[0].text;
const workerBuild = await build({
  entryPoints: [files.worker],
  platform: "browser", format: "iife", bundle: true, write: false, target: "es2022",
});
const workerScript = workerBuild.outputFiles[0].text;
const publicFiles = new Map([
  ["/tests/fixtures/geo-maplibre.html", {content: await readFile(path.join(root, "tests/fixtures/geo-maplibre.html")), type: "text/html; charset=utf-8"}],
  ["/dist/syntyr.core.css", {content: await readFile(path.join(root, "dist/syntyr.core.css")), type: "text/css; charset=utf-8"}],
  ["/dist/syntyr.geo.css", {content: await readFile(path.join(root, "dist/syntyr.geo.css")), type: "text/css; charset=utf-8"}],
  ["/maplibre-bundle.js", {content:script, type: "text/javascript; charset=utf-8"}],
  ["/maplibre-worker.js", {content:workerScript, type: "text/javascript; charset=utf-8"}],
]);
const server = createServer((req, res) => {
  const resource = publicFiles.get(req.url?.split("?")[0]);
  if (!resource) {res.writeHead(404);res.end("Not Found");return;}
  res.writeHead(200, {"Content-Type":resource.type, "Cache-Control":"no-store"});
  res.end(resource.content);
});
await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
const base = "http://127.0.0.1:" + server.address().port;
const browser = await chromium.launch({ headless:true, ...(process.env.SYNTYR_GEO_CHROMIUM_PATH ? {executablePath:process.env.SYNTYR_GEO_CHROMIUM_PATH} : {}), args:["--no-sandbox","--enable-webgl","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"] });
try {
  for (const width of [1280, 390, 320]) {
    const page = await browser.newPage({ viewport:{width,height:900} });
    const pageErrors = [];
    page.on("pageerror", error => pageErrors.push(error.message));
    await page.route("**/*", route => route.request().url().startsWith(base + "/") ? route.continue() : route.abort());
    await page.goto(base + "/tests/fixtures/geo-maplibre.html");
    await page.addStyleTag({path:files.css});
    await page.addScriptTag({url:base + "/maplibre-bundle.js"});
    await page.evaluate(() => {
      const map = new maplibregl.Map({
        container:"map",
        style:{version:8,sources:{},layers:[{id:"offline-background",type:"background",paint:{"background-color":"#c6dee2"}}]},
        center:[-73.9,40.7],zoom:8,attributionControl:false,cooperativeGestures:true,fadeDuration:0
      });
      window.__geoMap = map;
      const marker = document.createElement("button");
      marker.type = "button";
      marker.className = "syn-geo-marker";
      marker.setAttribute("aria-label","Inspect Site A");
      marker.dataset.synSelected="true";
      marker.addEventListener("click",()=>{marker.dataset.inspected="yes"});
      new maplibregl.Marker({element:marker}).setLngLat([-73.9,40.7]).addTo(map);
      document.querySelector("#geo-zoom").addEventListener("click",()=>map.zoomIn({duration:0}));
    });
    await page.waitForFunction(() => window.__geoMap?.loaded(), {timeout:12000});
    const before = await page.evaluate(()=>window.__geoMap.getZoom());
    await page.getByRole("button",{name:"Zoom in"}).click();
    const after = await page.evaluate(()=>window.__geoMap.getZoom());
    if (after <= before) throw new Error("Zoom click did not change MapLibre zoom: " + before + " -> " + after);
    await page.getByRole("button",{name:"Inspect Site A"}).click();
    if (await page.locator('[data-inspected="yes"]').count() !== 1) throw new Error("MapLibre marker click failed");
    await page.getByRole("button",{name:"Inspect Site A"}).focus();
    await page.keyboard.press("Enter");
    if (await page.locator('[data-inspected="yes"]').count() !== 1) throw new Error("Keyboard marker activation failed");

    const layout=await page.evaluate(()=>{
      const box=e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.width,r.height]};
      return {
        overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,
        columns:getComputedStyle(document.querySelector(".syn-geo-workspace")).gridTemplateColumns.trim().split(/\s+/).length,
        map:box(document.querySelector(".syn-geo-map")),
        marker:box(document.querySelector(".syn-geo-marker")),
        overlay:getComputedStyle(document.querySelector(".syn-geo-overlay")).pointerEvents,
        controls:getComputedStyle(document.querySelector(".syn-geo-controls")).pointerEvents
      };
    });
    if (layout.overflow>1) throw new Error(width + "px horizontal overflow: " + layout.overflow);
    if (layout.map[2]<=0 || layout.map[3]<=0) throw new Error(width+"px MapLibre mount collapsed");
    if (layout.marker[2]<44 || layout.marker[3]<44) throw new Error(width+"px marker target too small: "+layout.marker);
    if (layout.overlay!=="none" || layout.controls!=="auto") throw new Error("Overlay pointer events incorrect");
    if (width<=390 && layout.columns!==1) throw new Error(width+"px workspace did not stack: "+layout.columns);
    if (process.env.SYNTYR_GEO_SCREENSHOT_DIR) await page.screenshot({path:path.join(process.env.SYNTYR_GEO_SCREENSHOT_DIR,"syntyr-maplibre-"+width+".png"),fullPage:true});
    if (width === 1280) {
      for (const scale of [2, 4]) {
        await page.evaluate(s => { document.documentElement.style.fontSize = (16 * s) + "px"; }, scale);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        if (overflow > 1) throw new Error("Text reflow at " + scale + "x caused " + overflow + "px horizontal overflow");
      }
    }
    if (pageErrors.length) throw new Error("Uncaught browser errors: " + pageErrors.join("; "));
    await page.evaluate(()=>window.__geoMap.remove());
    await page.close();
    console.log("PASS MapLibre real render/zoom/marker/responsive at "+width+"px");
  }
} finally { await browser.close(); await new Promise(resolve => server.close(resolve)); }
