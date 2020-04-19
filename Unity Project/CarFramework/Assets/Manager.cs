using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Manager : MonoBehaviour
{
    public int popSize;
    public GameObject car;
    public GameObject spawn;
    private int port = 6000;
    public string managerPort;
    public bool callScript;
    public List<CarMove> activeCars = new List<CarMove>();
    public int generation = 0;
    // Start is called before the first frame update
    void Start()
    {
        print("Generating Cars");
        for (int i = 0; i < popSize; i++)
        {
            GameObject spawnedCar = car.transform.GetChild(i).gameObject;
            //GameObject spawnedCar = Instantiate(car, spawn.transform.position, Quaternion.identity);7
            spawnedCar.SetActive(true);
            spawnedCar.GetComponent<CarMove>().port = port.ToString();
            port += 1;
            activeCars.Add(spawnedCar.GetComponent<CarMove>());
        }

        if (callScript)
        {
            string strCmdText;
            strCmdText = $"/K py C:\\Users\\alext\\Documents\\GitHub\\dissertation\\neuralTesting\\NEAT\\NeatCore.py --population_size {popSize}";   //This command to open a new notepad
            System.Diagnostics.Process.Start("CMD.exe", strCmdText); //Start cmd process
        }        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void ReactivateCars()
    {
        for (int i = 0; i < activeCars.Count; i++)
        {
            activeCars[i].flaggedToRespawn = true;
        }
    }

    public void handleMessage(string msg)
    {
        print(msg);
        if(msg == "respawn")
        {
            ReactivateCars();
            generation++;
        }
    }
}
