using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

namespace running {


public class TcpListenerManager : MonoBehaviour
{
    Thread mThread;
    public string connectionIP = "127.0.0.1";
    public int connectionPort = 12345;
    IPAddress localAdd;
    TcpListener listener;
    TcpClient client;
    public static string dataReceived = "";
    private bool playing = true;

    public static TcpListenerManager instance;
    //private UnityChanControlScriptWithRgidBody unityChanControl;

    private void Awake()
    {
        // Ensure only one instance of the manager exists
        if (instance != null && instance != this)
        {
            Destroy(gameObject);
            return;
        }

        instance = this;
        DontDestroyOnLoad(gameObject);
    }

    private void Start()
    {

        
        ThreadStart ts = new ThreadStart(StartListener);
        mThread = new Thread(ts);
        mThread.Start();
    }

    private void OnDestroy()
    {
        // Stop the TCP listener when the persistent object is destroyed
        StopListener();
    }

    private void StartListener()
    {
        localAdd = IPAddress.Parse(connectionIP);
        listener = new TcpListener(IPAddress.Any, connectionPort);
        listener.Start();
        Debug.Log("listening");
        client = listener.AcceptTcpClient();
        playing = true;
        while (playing)
        {
            SendAndReceiveData();
        }
    }

    private void StopListener()
    {
        // Implement TCP listener cleanup and resource release here
        listener.Stop();
        listener = null;
    }




    void SendAndReceiveData()
{
    NetworkStream nwStream = client.GetStream();
    byte[] buffer = new byte[client.ReceiveBufferSize];

    int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
    dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead); //Converting byte data to string

    if (!string.IsNullOrEmpty(dataReceived))
    {
        // Print the received data
        Debug.Log("Received data: " + dataReceived);

        //---Sending Data to Host----
        string responseMessage = "Hey I got your message Python! Do You see this message?";
        byte[] myWriteBuffer = Encoding.ASCII.GetBytes(responseMessage); //Converting string to byte data
        nwStream.Write(myWriteBuffer, 0, myWriteBuffer.Length); //Sending the data in Bytes to Python



    }

   
}


}

}
