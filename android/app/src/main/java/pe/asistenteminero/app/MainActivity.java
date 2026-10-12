package pe.asistenteminero.app;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.core.content.FileProvider;
import androidx.webkit.ServiceWorkerClientCompat;
import androidx.webkit.ServiceWorkerControllerCompat;
import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewFeature;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

/**
 * Envuelve la app web (assets/www) en un WebView. Los archivos se sirven desde
 * https://appassets.androidplatform.net para que la página tenga origen seguro
 * (localStorage, IndexedDB y fetch a las API de IA funcionan igual que en el navegador).
 */
public class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final String START = "https://" + HOST + "/assets/www/index.html";
    private static final int PICK = 1;

    private WebView web;
    private WebViewAssetLoader loader;
    private ValueCallback<Uri[]> pending;
    private File photoFile;
    private Uri photoUri;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        loader = new WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        web = new WebView(this);
        setContentView(web);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false);

        if (WebViewFeature.isFeatureSupported(WebViewFeature.SERVICE_WORKER_BASIC_USAGE)
                && WebViewFeature.isFeatureSupported(WebViewFeature.SERVICE_WORKER_SHOULD_INTERCEPT_REQUEST)) {
            ServiceWorkerControllerCompat.getInstance().setServiceWorkerClient(new ServiceWorkerClientCompat() {
                @Override
                public WebResourceResponse shouldInterceptRequest(WebResourceRequest req) {
                    return loader.shouldInterceptRequest(req.getUrl());
                }
            });
        }

        web.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView v, WebResourceRequest req) {
                return loader.shouldInterceptRequest(req.getUrl());
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest req) {
                Uri u = req.getUrl();
                if (HOST.equals(u.getHost())) return false;
                // Enlaces externos (fuentes, AI Studio, otras IA) se abren en el navegador.
                try { startActivity(new Intent(Intent.ACTION_VIEW, u)); } catch (ActivityNotFoundException e) { }
                return true;
            }
        });

        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView v, ValueCallback<Uri[]> cb, FileChooserParams p) {
                if (pending != null) pending.onReceiveValue(null);
                pending = cb;
                try {
                    startActivityForResult(chooser(p.getMode() == FileChooserParams.MODE_OPEN_MULTIPLE), PICK);
                    return true;
                } catch (Exception e) {
                    pending = null;
                    return false;
                }
            }
        });

        if (state != null) web.restoreState(state);
        else web.loadUrl(START);
    }

    /** Selector de archivos (texto, PDF, imágenes) con la opción de tomar una foto. */
    private Intent chooser(boolean multiple) {
        Intent pick = new Intent(Intent.ACTION_GET_CONTENT);
        pick.addCategory(Intent.CATEGORY_OPENABLE);
        pick.setType("*/*");
        pick.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{"text/*", "application/pdf", "image/*"});
        if (multiple) pick.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);

        Intent chooser = Intent.createChooser(pick, "Agregar documento");
        photoFile = null;
        photoUri = null;
        try {
            File dir = new File(getCacheDir(), "fotos");
            dir.mkdirs();
            photoFile = new File(dir, "foto-" + System.currentTimeMillis() + ".jpg");
            photoUri = FileProvider.getUriForFile(this, "pe.asistenteminero.app.fotos", photoFile);
            Intent cam = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            cam.putExtra(MediaStore.EXTRA_OUTPUT, photoUri);
            cam.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION | Intent.FLAG_GRANT_READ_URI_PERMISSION);
            if (cam.resolveActivity(getPackageManager()) != null) {
                chooser.putExtra(Intent.EXTRA_INITIAL_INTENTS, new Intent[]{cam});
            }
        } catch (Exception e) {
            photoFile = null;
            photoUri = null;
        }
        return chooser;
    }

    @Override
    protected void onActivityResult(int req, int code, Intent data) {
        super.onActivityResult(req, code, data);
        if (req != PICK || pending == null) return;
        Uri[] result = null;
        if (code == RESULT_OK) {
            if (data != null && data.getClipData() != null) {
                List<Uri> uris = new ArrayList<>();
                for (int i = 0; i < data.getClipData().getItemCount(); i++) {
                    uris.add(data.getClipData().getItemAt(i).getUri());
                }
                result = uris.toArray(new Uri[0]);
            } else if (data != null && data.getData() != null) {
                result = new Uri[]{data.getData()};
            } else if (photoFile != null && photoFile.length() > 0) {
                result = new Uri[]{photoUri};
            }
        }
        pending.onReceiveValue(result);
        pending = null;
    }

    @Override
    protected void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        web.saveState(out);
    }

    @Override
    public void onBackPressed() {
        if (web.canGoBack()) web.goBack();
        else super.onBackPressed();
    }

    @Override
    protected void onPause() {
        super.onPause();
        web.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
    }
}
