using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using System.IO;
using WindowsInput.Native;
using WindowsInput;

/// <summary>
/// Handle the car movement and control
/// </summary>
public class CarMove : MonoBehaviour
{
    [Header("Probably less than ideal")]
    public string port;

    [Header("General")]
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

    public float fitness;
    public float timeAlive;
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
    float h;
    float v;

    public bool alive = true;
    public bool manualControl = false;

    Gradient g = new Gradient();

    InputSimulator sim = new InputSimulator();

    SpriteRenderer rend;

    public bool sendDeathMsg;
    public bool flaggedToRespawn = false;


    void Start()
    {
        spawnPos = transform.position;
        spawnRot = transform.localRotation;
        rb = GetComponent<Rigidbody2D>();

        // assign events
        if (offTrackEvent == null)
            offTrackEvent = new UnityEvent();

        offTrackEvent.AddListener(FellOffTrack);

        if (checkpointEvent == null)
            checkpointEvent = new UnityEvent();

        checkpointEvent.AddListener(CheckpointHit);

        // give colors to the sensors transitioning from red to blue
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

        // if saving data (for training data) call this function every 0.1 seconds
        if(outputValues)
            InvokeRepeating("SaveOutput", .5f, 0.1f);

        rend = GetComponent<SpriteRenderer>();
    }

    void FixedUpdate()
    {
        if (alive)
        {
            // hande movement 
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

            float driftForce = Vector2.Dot(rb.velocity, rb.GetRelativeVector(rightAngleFromForward.normalized));

            Vector2 relativeForce = (rightAngleFromForward.normalized * -1.0f) * (driftForce * 10.0f);            

            rb.AddForce(rb.GetRelativeVector(relativeForce));

            speed = rb.velocity.magnitude;
            angle = transform.rotation.eulerAngles.z;
            curSteering = h;
            curAcceleration = v;
        }

        // allow user input 
        if (manualControl)
        {
            h = -Input.GetAxis("Horizontal");
            v = Input.GetAxis("Vertical");
        }
    }

    private void Update()
    {        
        if (alive)
        {
            // calculate "fitness"
            fitness += (Time.deltaTime * 0.1f);
            timeAlive += Time.deltaTime;

            // kill if stale
            if (timeAlive > 20 && !(fitness > 15))
                handleDeath();


            // Sensor handling
            RaycastHit2D hit;

            // each ray rotated equally around 360 degrees
            var thetaAngle = 360 / (sensors);
            var startAngle = 360;

            var change = 1f / (sensors - 1);
            float start = 1f;

            for (int i = 0; i < sensors; i++)
            {
                hit = Physics2D.Raycast(transform.position, Quaternion.AngleAxis(startAngle, new Vector3(0, 0, 1)) * transform.up, checkDist, layerMask);
                distances[i] = hit.distance;
                if (hit.collider != null)
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

            //w = Input.GetKey(KeyCode.W) ? true : false;
            //s = Input.GetKey(KeyCode.S) ? true : false;
            //a = Input.GetKey(KeyCode.A) ? true : false;
            //d = Input.GetKey(KeyCode.D) ? true : false;
        }
        else
        {
            if (flaggedToRespawn)
            {
                handleRespawn();
            }
        }

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
        handleDeath();        
    }

    // increase fitness if hitting checkpoints
    void CheckpointHit()
    {
        print("Hit Checkpoint");
        fitness += 15;
    }

    // produce training data
    public void SaveOutput()
    {
        // create a format and assign inputs into it
        // slightly unnessisary but a little cleaner
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

        // format the data into a string for the CSV file
        string formatted = $"{format.Speed};{format.Angle};{format.Steering};{format.Acceleration};{format.Sensor1};{format.Sensor2};{format.Sensor3};{format.Sensor4};{format.Sensor5};{format.Sensor6};{format.W};{format.A};{format.S};{format.D}";

        // write the line into the file
        string docPath = "C:/Users/alext/PycharmProjects/neuralTesting";

        using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "TrainingData5.csv"), true))
        {
            outputFile.WriteLine(formatted);
        }

    }

    // get the current input data formatted nicely
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
        format.Alive = alive.ToString();
        format.CurrentFitness = fitness;

        //format.W = w;
        //format.S = s;
        //format.A = a;
        //format.D = d;

        string formatted = $"-a;{format.Speed};{format.Angle};{format.Steering};{format.Acceleration};{format.Sensor1};{format.Sensor2};{format.Sensor3};{format.Sensor4};{format.Sensor5};{format.Sensor6};{format.Alive};{format.CurrentFitness}";
        //print("sending: " + formatted);
        return formatted;
        //string docPath = "C:/Users/alext/PycharmProjects/neuralTesting";

        // Write the string array to a new file named "WriteLines.txt".
        //using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "TrainingData2.csv"), true))
        //{
        //    outputFile.WriteLine(formatted);
        //}
    }

    // retrieves the output from the server and activates the relevent input(s)
    public void handleMessage(string msg)
    {
        //w;a;s;d
        string[] inputs = msg.Split(';');

        if(float.Parse(inputs[0]) > activationThreshold)
        {
            //sim.Keyboard.KeyDown(VirtualKeyCode.VK_W);
            v = 1;
            w = true;
        }
        else
        {
            //sim.Keyboard.KeyUp(VirtualKeyCode.VK_W);
            if (float.Parse(inputs[1]) > activationThreshold)
            {
                //sim.Keyboard.KeyDown(VirtualKeyCode.VK_A);
                h = 1;
                a = true;

            }
            else
            {
                //sim.Keyboard.KeyUp(VirtualKeyCode.VK_A);
                h = 0;
                a = false;
            }
        }

        if (float.Parse(inputs[2]) > activationThreshold)
        {
            //sim.Keyboard.KeyDown(VirtualKeyCode.VK_S);
            v = -1;
            s = true;
        }
        else
        {
            //sim.Keyboard.KeyUp(VirtualKeyCode.VK_S);
            if (float.Parse(inputs[3]) > activationThreshold)
            {
                //sim.Keyboard.KeyDown(VirtualKeyCode.VK_D);
                h = -1;
                d = true;
            }
            else
            {
                //sim.Keyboard.KeyUp(VirtualKeyCode.VK_D);
                h = 0;
                d = false;
            }
        }
    }

    void handleDeath()
    {
        alive = false;
        rend.enabled = false;
        transform.position = spawnPos;
        transform.localRotation = spawnRot;
        rb.velocity = Vector2.zero;
        sendDeathMsg = true;
    }

    public void handleRespawn()
    {
        fitness = 0;
        timeAlive = 0;
        alive = true;
        rend.enabled = true;
        flaggedToRespawn = false;
    } 
}