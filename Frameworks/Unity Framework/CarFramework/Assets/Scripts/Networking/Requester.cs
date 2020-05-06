using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

/// <summary>
/// network client implementation to send and recieve data from a server
/// </summary>
public class Requester : RunAbleThread
{
    public CarMove carRef;
    public string port;

    public bool sendDeathMsg;

    RequestSocket client;

    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (client = new RequestSocket())
        {
            string connector = "tcp://localhost:";
            connector += port;
            client.Connect(connector);

            while (Running)
            {
                // send data
                client.SendFrame(carRef.OutputData());
                string message = null;
                bool gotMessage = false;
                while (Running)
                {
                    gotMessage = client.TryReceiveFrameString(out message); // this returns true if it's successful
                    if (gotMessage) break;
                }

                if (gotMessage)
                {
                    // send the message to the car to handle
                    Debug.Log($"{message} port {port}");
                    carRef.handleMessage(message);
                }                  
                
            }
        }

        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}