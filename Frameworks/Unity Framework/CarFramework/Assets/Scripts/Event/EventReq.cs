using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

/// <summary>
/// copy of previous client, modified to send different data and handle for ease
/// </summary>
public class EventReq : RunAbleThread
{
    public string port;
    public Manager managerRef;
    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
            string connector = "tcp://localhost:";
            connector += port;
            client.Connect(connector);            

            while (Running)
            {
                client.SendFrame("");

                string message = null;
                bool gotMessage = false;
                while (Running)
                {
                    gotMessage = client.TryReceiveFrameString(out message); // this returns true if it's successful
                    if (gotMessage) break;
                }

                if (gotMessage)
                {
                    //Debug.Log("Received " + message);
                    managerRef.handleMessage(message);
                }
                
            }
        }

        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}