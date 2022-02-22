using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spawner : MonoBehaviour {
    public GameObject obstacle;

    //clones are created so that the obstacles can be destroyed once assigned to a clone.
    private GameObject clone1; 
    private GameObject clone2;

    private float timeSinceSpawn;
    public float timeBetweenSpawn;
    public float lifeTime;


    public float GapSize;
    public float GapMaxHeight;

    public int gamestart = 0;
    
    // Update is called once per frame
    private void Update() {
        if (Input.GetButtonDown("Jump")){
            gamestart = 1;
        }
        

        if(gamestart == 1){
            if(timeSinceSpawn <= 0){
                //spawn(what, where, rotation);
                float random = Random.Range(-GapMaxHeight, GapMaxHeight);
                clone1 = Instantiate(obstacle, transform.position + new Vector3(0, GapSize + random, 0), Quaternion.identity);
                clone2 = Instantiate(obstacle, transform.position + new Vector3(0, -GapSize + random, 0), Quaternion.identity);
                
                timeSinceSpawn = timeBetweenSpawn;
                //totalBarriersCreated++;
            } else {
                timeSinceSpawn -= Time.deltaTime;
            }
        }
        
        Destroy(clone1, lifeTime);
        Destroy(clone2, lifeTime);
    }
}
