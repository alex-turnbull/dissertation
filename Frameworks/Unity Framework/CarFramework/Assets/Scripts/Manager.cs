using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// controls and handles the agents and calling of script
/// </summary>
public class Manager : MonoBehaviour
{
    public int popSize;
    public GameObject car;
    public GameObject spawn;
    private int port = 6000;
    public string managerPort;
    public bool callScript;
    public string scriptDirectory;
    public List<CarMove> activeCars = new List<CarMove>();
    public int generation = 0;
    // Start is called before the first frame update
    void Start()
    {
        print("Generating Cars");
        // activate the required number of cars and assign ports
        for (int i = 0; i < popSize; i++)
        {
            GameObject spawnedCar = car.transform.GetChild(i).gameObject;
            spawnedCar.SetActive(true);
            spawnedCar.GetComponent<CarMove>().port = port.ToString();
            port += 1;
            activeCars.Add(spawnedCar.GetComponent<CarMove>());
        }

        // call the command line to run the Python
        if (callScript)
        {
            string strCmdText;
            strCmdText = $"/K py {scriptDirectory} --population_size {popSize}";   //This command to open a new notepad
            System.Diagnostics.Process.Start("CMD.exe", strCmdText); //Start cmd process
        }        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void ReactivateCars()
    {
        // tell the car it's ready to respawn
        for (int i = 0; i < activeCars.Count; i++)
        {
            activeCars[i].flaggedToRespawn = true;
        }
    }

    // recieve messages from event server and handle as such
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
