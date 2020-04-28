using UnityEngine;

public class EventClient : MonoBehaviour
{
    private EventReq _helloRequester;
    public Manager manager;

    private void Start()
    {
        _helloRequester = new EventReq();
        _helloRequester.managerRef = manager;
        _helloRequester.port = manager.managerPort;
        _helloRequester.Start();        
    }

    private void OnDestroy()
    {
        _helloRequester.Stop();
    }

    private void OnDisable()
    {
        _helloRequester.Stop();
    }
}