import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'vite';

test('SvelteKit renders and handles native HTML form POSTs without client scripts', async () => {
  const server = await createServer({
    server: { host: '127.0.0.1', port: 0, strictPort: true }
  });
  try {
    await server.listen();
    const { port } = server.httpServer.address();
    const url = `http://127.0.0.1:${port}/settings`;

    const get = await fetch(url, { headers: { Accept: 'text/html' } });
    const initial = await get.text();
    assert.equal(get.status, 200);
    assert.match(initial, /method="POST"/);
    assert.match(initial, /name="name"/);
    assert.match(initial, /syn-detail-layout/);

    async function post(value) {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          Origin: new URL(url).origin,
          Accept: 'text/html',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ name: value })
      });
      return { status: response.status, html: await response.text() };
    }

    const invalid = await post('x');
    assert.equal(invalid.status, 400);
    assert.match(invalid.html, /Check the submitted details/);
    assert.match(invalid.html, /Use at least 2 characters/);
    assert.match(invalid.html, /aria-invalid="true"/);
    assert.match(invalid.html, /aria-describedby="workspace-help workspace-error"/);

    const valid = await post('  Example Workspace  ');
    assert.equal(valid.status, 200);
    assert.match(valid.html, /Example Workspace/);
    assert.match(valid.html, /passed server validation/);

    const escaped = await post('<script>alert(1)</script>');
    assert.equal(escaped.status, 200);
    assert.match(escaped.html, /&lt;script>alert\(1\)&lt;\/script>/);
    assert.doesNotMatch(escaped.html, /<script>alert\(1\)<\/script>/);

    // SvelteKit intentionally enforces its origin-based CSRF check only in
    // production; the development server must not be used to test that gate.
  } finally {
    await server.close();
  }
});
