using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerMovement : MonoBehaviour {
    public Rigidbody2D rb;
    
    public float gravity = 2f;
    public float jumpSpeed = 10f;
    public float rotation = 1f;
    public int MinYCoordinate = -6;
    public float deathToRestartTime;
    
    // Start is called before the first frame update
    void Start()
    {
        //Physics2D.gravity = new Vector2(0,-10);//only awake once jump is called.
    }

    // Update is called once per frame
    void Update() {
        //Rotation
        transform.eulerAngles = new Vector3(0, 0, rb.velocity.y*rotation);
        
        //Jump
        if (Input.GetButtonDown("Jump")){
            rb.velocity = Vector2.up * jumpSpeed;
            rb.gravityScale = gravity;
        }

        if (rb.transform.position.y < MinYCoordinate) {
            SceneManager.LoadScene("Flappy Hex");
        }
    }

    //This class works because "is trigger" was checked in "Box Collider 2D".
    void OnTriggerEnter2D(Collider2D detected){
        if (detected.CompareTag("ObstacleTag")){
            enabled = false;
            StartCoroutine(DelayedRestart());
        }
    }

    IEnumerator DelayedRestart() {
        yield return new WaitForSeconds(deathToRestartTime);
        SceneManager.LoadScene("Flappy Hex");
    }
}
