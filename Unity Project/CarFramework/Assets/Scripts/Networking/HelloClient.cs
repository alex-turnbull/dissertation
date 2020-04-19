﻿using UnityEngine;

public class HelloClient : MonoBehaviour
{
    public HelloRequester _helloRequester;

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

    private void OnDisable()
    {
        _helloRequester.Stop();
    }
}