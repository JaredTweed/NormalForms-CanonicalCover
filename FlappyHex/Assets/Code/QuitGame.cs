using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class QuitGame : MonoBehaviour {
    
    void Update() {
        if (Input.GetKey("q")) {
            //Debug.Log("Application Quit");
            Application.Quit();
        }
    }
}
