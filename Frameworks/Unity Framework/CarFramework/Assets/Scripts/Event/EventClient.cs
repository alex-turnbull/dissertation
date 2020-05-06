using UnityEngine;

/// <summary>
/// setup event client
/// </summary>
public class EventClient : MonoBehaviour
{
    private EventReq _eventReq;
    public Manager manager;

    private void Start()
    {
        _eventReq = new EventReq();
        _eventReq.managerRef = manager;
        _eventReq.port = manager.managerPort;
        _eventReq.Start();        
    }

    private void OnDestroy()
    {
        _eventReq.Stop();
    }

    private void OnDisable()
    {
        _eventReq.Stop();
    }
}