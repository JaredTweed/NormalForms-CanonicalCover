using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TextFadeOut : MonoBehaviour
{
    public Text text;
    public float fadeLength = 0.75f;

    void Start()
    {
        text.canvasRenderer.SetAlpha(1.0f);
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetButtonDown("Jump")){
            text.CrossFadeAlpha(0.0f, fadeLength, false);
        }
    }
}
