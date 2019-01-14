package com.example.carol.wifi_camera;

/**
 * Created by carol on 17/06/2017.
 */

//import MyInterface;

public class Animal {
    private String aName;
    private String aSpeak;
    private int aIcon;

    public Animal() {
    }

    public Animal(String name,String aSpeak,int aIcon){
        this.aName = name;
        this.aSpeak = aSpeak;
        this.aIcon = aIcon;
    }
    public String getaName(){
        return aName;
    }
    public String getaSpeak(){
        return aSpeak;
    }
    public int getaIcon(){
        return aIcon;
    }

    public void speak(MyInterface myInterface){

        myInterface.MyInterfaceCallback();
    }




}



