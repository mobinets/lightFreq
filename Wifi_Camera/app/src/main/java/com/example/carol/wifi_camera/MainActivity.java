package com.example.carol.wifi_camera;

import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Toast;

import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;


@RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
public class MainActivity extends AppCompatActivity {




    public void createFile() {
        try {
            String path = Environment.getExternalStorageDirectory().getAbsolutePath();
            String str = "" + path + "/wifipython/";
            Log.v("NewFilePath", str);
            //Log.v("PAth",""+Environment.get);
            String oldPath = "" + Environment.getDataDirectory()+"/app/src/java/HelloWorld.py";
            File newPath = new File(str);
            File oldFile = new File(oldPath);
            if (!newPath.exists()) {

                newPath.mkdirs();
                Log.v("MakeDir", "true");
            }



            InputStream in = new FileInputStream(oldPath);
            FileOutputStream out = new FileOutputStream(newPath);
            byte[] data = new byte[1024];
            out.write(data, 0, data.length);
        }catch (FileNotFoundException e1){
            e1.printStackTrace();
        }catch (IOException e2){
            e2.printStackTrace();
        }
    }




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        NdkJniUtils jni = new






    }






