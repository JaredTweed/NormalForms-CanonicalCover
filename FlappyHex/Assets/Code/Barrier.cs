using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Barrier : MonoBehaviour
{
    public float speed;
    
    private void Update(){
        transform.Translate(Vector2.left * speed * Time.deltaTime);
    }
        
    
}
