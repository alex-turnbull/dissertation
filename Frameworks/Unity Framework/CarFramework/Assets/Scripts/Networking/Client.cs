using UnityEngine;

/// <summary>
/// create the client
/// </summary>
public class Client : MonoBehaviour
{
    public Requester _Requester;

    private void Start()
    {
        _Requester = new Requester();
        _Requester.carRef = gameObject.GetComponent<CarMove>();
        _Requester.port = gameObject.GetComponent<CarMove>().port;
        _Requester.Start();        
    }

    private void OnDestroy()
    {
        _Requester.Stop();
    }

    private void OnDisable()
    {
        _Requester.Stop();
    }
}