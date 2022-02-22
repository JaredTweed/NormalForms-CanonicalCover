using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TextFadeIn : MonoBehaviour
{
    public Text text;
    public float delay = 1.5f;
    public float fadeLength = 0.75f;

    void Start()
    {
        text.canvasRenderer.SetAlpha(0.0f);
        
    }

    // Update is called once per frame
    void Update() {
        if (Input.GetButtonDown("Jump")){
            StartCoroutine(FadeIn());
        }
    }

    IEnumerator FadeIn() {
        yield return new WaitForSeconds(delay);
        text.CrossFadeAlpha(1.0f, fadeLength, false);
    }
}