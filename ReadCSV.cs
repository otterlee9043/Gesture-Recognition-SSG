using System.Collections.Generic;
using System.IO;
using System;
using UnityEngine;

public class ReadCSV : MonoBehaviour {
    List<double[]> wrist_list = new List<double[]>();
    List<double[]> back_rlist = new List<double[]>();
    List<double[]> back_plist = new List<double[]>();
    List<string> outputString = new List<string>();
    private double[][] wrist_move;
    private double[][] back_rotate;
    private double[][] back_move;
    Quaternion back_rotation;

    public GameObject Hand;
    public GameObject Back;
    public GameObject LocalHand;
    public GameObject BackToHand;
    //public GameObject TracePrefab;
    bool stopLoop = false;
    int i = 0;

    public double[][] Convert_list(List<double[]> listToConvert) {
        return listToConvert.ToArray();
    } 

    private void Awake()
    {
        using (var reader = new StreamReader(@"circle_sskim01_rigidbody.csv"))
        {
            string[] values = null;
            string[] former_values = null;

            int wrist_idx = -1;
            int back_idx = -1;

            values = reader.ReadLine().Split(',');
            double[] double_values = new double[values.Length];
            for (int i = 0; i < values.Length; ++i)
            {
                Debug.LogFormat("{0}번째", i);
                if (wrist_idx == -1 && values[i].Contains("wrist")) wrist_idx = i;
                else if (back_idx == -1 && values[i].Contains("back")) back_idx = i;
                else if (wrist_idx > -1 && back_idx > -1) break;
            }
            reader.ReadLine();
            reader.ReadLine();

            while (!reader.EndOfStream)
            {
                try
                {
                    values = reader.ReadLine().Split(',');
                    for(int j = 0; j< values.Length; j++) double_values[j] = double.Parse(values[j]);
                    former_values = values;
                }
                catch {
                    Debug.Log("catch");
                    values = former_values;
                    for (int j = 0; j < former_values.Length; j++) double_values[j] = double.Parse(former_values[j]);
                }
                double[] temp_wrist_list = { double_values[wrist_idx + 0], double_values[wrist_idx + 1], double_values[wrist_idx + 2] };
                wrist_list.Add(temp_wrist_list);
                double[] temp_back_rotation_list = { double_values[back_idx + 0], double_values[back_idx + 1], double_values[back_idx + 2], double_values[back_idx + 3] };
                back_rlist.Add(temp_back_rotation_list);
                double[] temp_back_position_list = { double_values[back_idx + 4], double_values[back_idx + 5], double_values[back_idx + 6] };
                back_plist.Add(temp_back_position_list);
            }
        }
        
    }

    private void Start()
    {
        wrist_move = Convert_list(wrist_list);
        back_rotate = Convert_list(back_rlist);
        back_move = Convert_list(back_plist);
    }

    void Update()
    {
        int count = 0;
        while (count < 10 && stopLoop == false)
        {
            if (i == wrist_move.Length - 1)
            {
                stopLoop = true;
                WriteCSVFile();
            }
            Hand.transform.position = new Vector3((float)wrist_move[i][0], (float)wrist_move[i][1], (float)wrist_move[i][2]);
            Back.transform.position = new Vector3((float)back_move[i][0], (float)back_move[i][1], (float)back_move[i][2]);

            back_rotation = new Quaternion((float)back_rotate[i][0], (float)back_rotate[i][1], (float)back_rotate[i][2], (float)back_rotate[i][3]);
            var R = Matrix4x4.Rotate(back_rotation);
            var x_axis = R.GetColumn(0);
            var y_axis = R.GetColumn(1);
            var z_axis = R.GetColumn(2);

            //Debug.DrawLine(Back.transform.position, Back.transform.position + new Vector3(x_axis[0], x_axis[1], x_axis[2]), Color.red);
            //Debug.DrawLine(Back.transform.position, Back.transform.position + new Vector3(y_axis[0], y_axis[1], y_axis[2]), Color.blue);
            //Debug.DrawLine(Back.transform.position, Back.transform.position + new Vector3(z_axis[0], z_axis[1], z_axis[2]), Color.green);
            //BackToHand.transform.position = Hand.transform.position - Back.transform.position;
            LocalHand.transform.position = R.transpose * (Hand.transform.position - Back.transform.position);
            localPositionObj.transform.localPosition = Hand.transform.localPosition;
            LocalHand.transform.localPosition = Hand.transform.position;

            //var r = matrix4x4.rotate(quaternion);
            //local = r.transpose * (hand - back);
            if (i % 20 == 0) Instantiate(TracePrefab, LocalHand.transform.position, LocalHand.transform.rotation);
            count++;
            i++;
            //Debug.LogFormat("x:{0},y:{1},z:{2}", LocalHand.transform.position.x, LocalHand.transform.position.y, LocalHand.transform.position.z);
            string outputLine = String.Format("{0},{1},{2}",LocalHand.transform.position.x, LocalHand.transform.position.y, LocalHand.transform.position.z);
            outputString.Add(outputLine);
        }
        Debug.LogFormat("i : {0}", i);
    }

    public void WriteCSVFile()
    {
        using (StreamWriter outputFile = new StreamWriter("C:\\Users\\suagu\\Documents\\SSG\\Input_Data.csv"))
        {
            foreach (string line in outputString)
                outputFile.WriteLine(line);
        }
    }
}

