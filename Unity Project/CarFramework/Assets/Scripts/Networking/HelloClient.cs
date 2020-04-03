using UnityEngine;

public class HelloClient : MonoBehaviour
{
    private HelloRequester _helloRequester;

    private void Start()
    {
        _helloRequester = new HelloRequester();
        _helloRequester.carRef = gameObject.GetComponent<CarMove>();
        _helloRequester.port = gameObject.GetComponent<CarMove>().port;
        _helloRequester.Start();        
    }

    private void OnDestroy()
    {
        _helloRequester.Stop();
    }
}