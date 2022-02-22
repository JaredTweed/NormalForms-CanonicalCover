using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using UnityEngine.UI;

public class Counter : MonoBehaviour
{
    public GameObject theSpawner;
    private Spawner spawnerScript;

    public Text scoreText;
    
    public float timeSinceCount;
    private int scoreCount = 0;
    
    // Start is called before the first frame update
    void Start() {
        scoreText.text = "0";
        spawnerScript = theSpawner.GetComponent<Spawner>();
    }

    // Update is called once per frame
    void Update() {
        scoreText.text = scoreCount.ToString();

        if(spawnerScript.gamestart == 1){
            if(timeSinceCount <= 0){
                timeSinceCount = spawnerScript.timeBetweenSpawn;
                scoreCount++;
            } else {
                timeSinceCount -= Time.deltaTime;
            }
        }
    }
    
}
