package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func request(method, path string) *httptest.ResponseRecorder {
	r := httptest.NewRecorder()
	newHandler("../../dist").ServeHTTP(r, httptest.NewRequest(method, path, nil))
	return r
}

func TestEscapedNativeComponentComposition(t *testing.T) {
	res := request(http.MethodGet, "/?q=%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E")
	if res.Code != http.StatusOK {
		t.Fatalf("GET: %d", res.Code)
	}
	body := res.Body.String()
	for _, want := range []string{`class="syn-root`, `class="syn-field`, `class="syn-input"`, `class="syn-button`, `class="syn-alert`, `&lt;img`, `method="get"`, `aria-label="Resource pages"`} {
		if !strings.Contains(body, want) {
			t.Errorf("missing %q", want)
		}
	}
	if strings.Contains(body, `<img src=x`) || strings.Contains(body, "<script") {
		t.Fatal("unsafe or unexpected active markup")
	}
	if !strings.Contains(request(http.MethodGet, "/").Body.String(), `class="syn-table`) {
		t.Fatal("expected table on unfiltered search")
	}
}

func TestServerValidationLinksFieldError(t *testing.T) {
	res := request(http.MethodGet, "/?q="+strings.Repeat("a", 81))
	if res.Code != http.StatusBadRequest {
		t.Fatalf("want 400, got %d", res.Code)
	}
	body := res.Body.String()
	for _, want := range []string{`aria-invalid="true"`, `aria-describedby="resource-query-error"`, `id="resource-query-error"`, `role="alert"`, `data-syn-state="error"`} {
		if !strings.Contains(body, want) {
			t.Errorf("missing %q", want)
		}
	}
}

func TestPaginationPreservesEncodedFilter(t *testing.T) {
	res := request(http.MethodGet, "/?q=%26&page=1")
	if res.Code != http.StatusOK {
		t.Fatalf("GET: %d", res.Code)
	}
	body := res.Body.String()
	if !strings.Contains(body, `name="q"`) || !strings.Contains(body, `value="&amp;"`) {
		t.Fatal("query not preserved safely")
	}
	if !strings.Contains(body, `href="/?page=2&amp;q=%26"`) {
		t.Fatal("pagination did not preserve encoded query")
	}
	if strings.Contains(body, `href="/?q=&`) {
		t.Fatal("query was not encoded in link")
	}
	res = request(http.MethodGet, "/?page=2")
	if res.Code != http.StatusOK {
		t.Fatalf("page 2: %d", res.Code)
	}
	body = res.Body.String()
	for _, want := range []string{`aria-current="page"`, `href="/"`, `href="/?page=3"`} {
		if !strings.Contains(body, want) {
			t.Errorf("missing %q", want)
		}
	}
}

func TestInvalidPageAndMethods(t *testing.T) {
	for _, path := range []string{"/?page=zero", "/?page=-1", "/?page=999"} {
		if got := request(http.MethodGet, path).Code; got != http.StatusBadRequest {
			t.Errorf("%s: got %d", path, got)
		}
	}
	if got := request(http.MethodPost, "/"); got.Code != http.StatusMethodNotAllowed || got.Header().Get("Allow") != "GET, HEAD" {
		t.Fatalf("POST: %d %s", got.Code, got.Header().Get("Allow"))
	}
	if got := request(http.MethodGet, "/unknown").Code; got != http.StatusNotFound {
		t.Fatalf("unknown: %d", got)
	}
	if res := request(http.MethodHead, "/"); res.Code != http.StatusOK {
		t.Fatalf("HEAD: %d", res.Code)
	}
}
