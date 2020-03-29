using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using System.IO;
using WindowsInput.Native;
using WindowsInput;

public class CarMove : MonoBehaviour
{
    public float acceleration;
    public float steering;
    private Rigidbody2D rb;

    public LayerMask layerMask;

    UnityEvent offTrackEvent;
    UnityEvent checkpointEvent;

    public int sensors;
    public float checkDist;

    public float activationThreshold;

    Vector3 spawnPos;
    Quaternion spawnRot;

    public bool outputValues;
    public string outputFile;
    Vector2 speeds;

    [Header("Output Values")]
    public float speed;
    public float angle;
    public float curSteering;
    public float curAcceleration;
    public float[] distances;
    public bool w;
    public bool s;
    public bool a;
    public bool d;

    Gradient g = new Gradient();

    InputSimulator sim = new InputSimulator();

    void Start()
    {
        spawnPos = transform.position;
        spawnRot = transform.localRotation;
        rb = GetComponent<Rigidbody2D>();

        if (offTrackEvent == null)
            offTrackEvent = new UnityEvent();

        offTrackEvent.AddListener(FellOffTrack);

        if (checkpointEvent == null)
            checkpointEvent = new UnityEvent();

        checkpointEvent.AddListener(CheckpointHit);

        
        GradientColorKey[] gck = new GradientColorKey[2];
        GradientAlphaKey[] gak = new GradientAlphaKey[2];
        gck[0].color = Color.red;
        gck[0].time = 1.0F;
        gck[1].color = Color.blue;
        gck[1].time = -1.0F;
        gak[0].alpha = 1.0F;
        gak[0].time = 1.0F;
        gak[1].alpha = 1.0F;
        gak[1].time = -1.0F;
        g.SetKeys(gck, gak);

        if(outputValues)
            InvokeRepeating("SaveOutput", .5f, 0.1f);
        //POLL DATA AND SEND TO SERVER HERE ^^
    }

    void FixedUpdate()
    {
        float h = -Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");

        speeds = transform.up * (v * acceleration);
        rb.AddForce(speeds);

        float direction = Vector2.Dot(rb.velocity, rb.GetRelativeVector(Vector2.up));
        if (direction >= 0.0f)
        {
            rb.rotation += h * steering * (rb.velocity.magnitude / 5.0f);
            //rb.AddTorque((h * steering) * (rb.velocity.magnitude / 10.0f));
        }
        else
        {
            rb.rotation -= h * steering * (rb.velocity.magnitude / 5.0f);
            //rb.AddTorque((-h * steering) * (rb.velocity.magnitude / 10.0f));
        }

        Vector2 forward = new Vector2(0.0f, 0.5f);
        float steeringRightAngle;
        if (rb.angularVelocity > 0)
        {
            steeringRightAngle = -90;
        }
        else
        {
            steeringRightAngle = 90;
        }

        Vector2 rightAngleFromForward = Quaternion.AngleAxis(steeringRightAngle, Vector3.forward) * forward;
        //Debug.DrawLine((Vector3)rb.position, (Vector3)rb.GetRelativePoint(rightAngleFromForward), Color.green);

        float driftForce = Vector2.Dot(rb.velocity, rb.GetRelativeVector(rightAngleFromForward.normalized));
   
        Vector2 relativeForce = (rightAngleFromForward.normalized * -1.0f) * (driftForce * 10.0f);


        //Debug.DrawLine((Vector3)rb.position, (Vector3)rb.GetRelativePoint(relativeForce), Color.red);

        rb.AddForce(rb.GetRelativeVector(relativeForce));

        speed = rb.velocity.magnitude;
        angle = transform.rotation.eulerAngles.z;
        curSteering = h;
        curAcceleration = v;       
    }

    private void Update()
    {
        RaycastHit2D hit;

        var thetaAngle = 360 / (sensors);
        var startAngle = 360;

        var change = 1f / (sensors - 1);
        float start = 1f;

        for (int i = 0; i < sensors; i++)
        {
            hit = Physics2D.Raycast(transform.position, Quaternion.AngleAxis(startAngle, new Vector3(0, 0, 1)) * transform.up, checkDist, layerMask);
            distances[i] = hit.distance;
            if(hit.collider != null)
            {
                Debug.DrawLine(transform.position, hit.point, g.Evaluate(start));
            }
            else
            {
                Debug.DrawRay(transform.position, Quaternion.AngleAxis(startAngle, new Vector3(0, 0, 1)) * transform.up * checkDist, g.Evaluate(start));
            }
            startAngle -= thetaAngle;
            start -= change;
        }
        //Debug.DrawRay(transform.position, transform.up, Color.red);

        // If it hits something...
        //if (hit.collider != null)
        //{
        //    Debug.DrawLine(transform.position, hit.point, Color.white);
        //}   

        w = Input.GetKey(KeyCode.W) ? true : false;
        s = Input.GetKey(KeyCode.S) ? true : false;
        a = Input.GetKey(KeyCode.A) ? true : false;
        d = Input.GetKey(KeyCode.D) ? true : false;
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if(collision.tag == "track")
        {
            offTrackEvent.Invoke();
            
        }
        else if(collision.tag == "checkpoint")
        {
            checkpointEvent.Invoke();
        }
    }

    void FellOffTrack()
    {
        transform.position = spawnPos;
        transform.localRotation = spawnRot;
        rb.velocity = Vector2.zero;
    }

    void CheckpointHit()
    {
        print("Hit Checkpoint");
    }

    public void SaveOutput()
    {
        DataFormat format = new DataFormat();
        format.Speed = speed;
        format.Angle = angle;
        format.Steering = curSteering;
        format.Acceleration = curAcceleration;
        format.Sensor1 = distances[0];
        format.Sensor2 = distances[1];
        format.Sensor3 = distances[2];
        format.Sensor4 = distances[3];
        format.Sensor5 = distances[4];
        format.Sensor6 = distances[5];

        format.W = w;
        format.S = s;
        format.A = a;
        format.D = d;

        string formatted = $"{format.Speed};{format.Angle};{format.Steering};{format.Acceleration};{format.Sensor1};{format.Sensor2};{format.Sensor3};{format.Sensor4};{format.Sensor5};{format.Sensor6};{format.W};{format.A};{format.S};{format.D}";


        string docPath = "C:/Users/alext/PycharmProjects/neuralTesting";

        //Write the string array to a new file named "WriteLines.txt".
        using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "TrainingData5.csv"), true))
        {
            outputFile.WriteLine(formatted);
        }

    }

    public string OutputData()
    {
        DataFormat format = new DataFormat();
        format.Speed = speed;
        format.Angle = angle;
        format.Steering = curSteering;
        format.Acceleration = curAcceleration;
        format.Sensor1 = distances[0];
        format.Sensor2 = distances[1];
        format.Sensor3 = distances[2];
        format.Sensor4 = distances[3];
        format.Sensor5 = distances[4];
        format.Sensor6 = distances[5];

        //format.W = w;
        //format.S = s;
        //format.A = a;
        //format.D = d;

        string formatted = $"{format.Speed};{format.Angle};{format.Steering};{format.Acceleration};{format.Sensor1};{format.Sensor2};{format.Sensor3};{format.Sensor4};{format.Sensor5};{format.Sensor6}";
        return formatted;
        //string docPath = "C:/Users/alext/PycharmProjects/neuralTesting";

        // Write the string array to a new file named "WriteLines.txt".
        //using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "TrainingData2.csv"), true))
        //{
        //    outputFile.WriteLine(formatted);
        //}
    }

    public void handleMessage(string msg)
    {
        //w;a;s;d
        string[] inputs = msg.Split(';');

        if(float.Parse(inputs[0]) > activationThreshold)
        {
            sim.Keyboard.KeyDown(VirtualKeyCode.VK_W);
        }
        else
        {
            sim.Keyboard.KeyUp(VirtualKeyCode.VK_W);
        }

        if (float.Parse(inputs[1]) > activationThreshold)
        {
            sim.Keyboard.KeyDown(VirtualKeyCode.VK_A);
        }
        else
        {
            sim.Keyboard.KeyUp(VirtualKeyCode.VK_A);
        }

        if (float.Parse(inputs[2]) > activationThreshold)
        {
            sim.Keyboard.KeyDown(VirtualKeyCode.VK_S);
        }
        else
        {
            sim.Keyboard.KeyUp(VirtualKeyCode.VK_S);
        }

        if (float.Parse(inputs[3]) > activationThreshold)
        {
            sim.Keyboard.KeyDown(VirtualKeyCode.VK_D);
        }
        else
        {
            sim.Keyboard.KeyUp(VirtualKeyCode.VK_D);
        }

    }
}