using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AD_GUI
{
    public partial class Form1 : Form
    {
        // Indata Vorbereitung
        public delegate void d1(string indata);

        // Boolsche Werte zur Statusabfrage im Ablauf
        private bool connected = false;
        private bool kalibriert = false;
        private bool titration = false;
        private bool gestoppt = false;
        private bool resettet = true;
        private int durchlauf = 0;

        // Messwerte
        private double menge_kalib = 0;
        private string[] Farbe;
        private int Zeit1 = 0;

        // Schrittzähler
        private readonly double kalibrierschritte = 7500;
        private double stepcounter = 0;
        private double m_aktuell = 0;

        public Form1()
        {
            InitializeComponent();
        }

        // Hier wird die Fenstergröße festgelegt
        private void Form1_Load(object sender, EventArgs e)
        {
            this.Width = 1600;
            this.Height = 920;
            
        }
        // Hier wird der Port festgelegt
        private void button9_Click(object sender, EventArgs e)
        {
            string portname = textBox2.Text;
            if (serialPort1.IsOpen != true)
            {
                try
                {
                    serialPort1.PortName = portname;
                    serialPort1.Open();
                    connected = true;
                    Fehlermeldung.Text = "(Meldungen)";
                }
                catch
                {
                    Fehlermeldung.Text = "Port konnte nicht gefunden werden";
                }
            }
            else
            {
                Fehlermeldung.Text = "Port ist bereits verbunden";
            }
        }
        // Vorwärts Button
        private void button1_Click(object sender, EventArgs e)
        {
            if (connected)
            {
                serialPort1.Write("F");
                Phasenlabel.Text = "Suche die Position, an der die Spritze Kontakt zum Schieber der Pumpe und " +
                    "gleichzeitig möglichst viel Inhalt hat.";
            }
        }
        // Rückwärts Button
        private void button2_Click(object sender, EventArgs e)
        {
            if (connected)
            {
                serialPort1.Write("B");
                Phasenlabel.Text = "Suche die Position, an der die Spritze Kontakt zum Schieber der Pumpe und " +
                    "gleichzeitig möglichst viel Inhalt hat.";
            }
        }
        // Nullposition Button
        private void button5_Click(object sender, EventArgs e)
        {
            if (connected)
            {
                serialPort1.Write("N");
            }
        }
        // Befehl an den Arduino die Kalibrierung zu starten
        private void button3_Click(object sender, EventArgs e)
        {
            if (connected)
            {
                if (tariert.Checked)
                {
                    serialPort1.Write("K");
                    kalibriert = true;
                }
                else
                {
                    Fehlermeldung.Text = "Checke, ob Waage tariert ist";
                }
            }
        }
        // Eingabe des Messwertes nach Kalibrierung
        private void button4_Click(object sender, EventArgs e)
        {
            if (kalibriert)
            {
                string swert = textBox1.Text;

                swert.Replace('.', ',');

                try
                {
                    double dwert = Convert.ToDouble(swert);
                    menge_kalib = dwert/kalibrierschritte;

                    groupBox4.Enabled = true;
                    groupBox2.Enabled = false;
                    groupBox1.Enabled = true;

                    if (Fehlermeldung.Text == "Überprüfe die Eingabe für die Masse")
                    {
                        Fehlermeldung.Text = "(Meldungen)";
                    }
                }
                catch
                {
                    Fehlermeldung.Text = "Überprüfe die Eingabe für die Masse";
                }
            }
        }

        // Datenannahme vom SerialPort
        private void serialPort1_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
                string indata = serialPort1.ReadLine();
                d1 writeit = new d1(Write2Form);
                Invoke(writeit, indata);
        }
        // Datenverarbeitung aus den Port-Befehlen
        public void Write2Form(string indata)
        {
            char firstchar;
            firstchar = indata[0];
            switch (firstchar)
            {
                case 's':
                    string zahl = indata.Replace("s", "");
                    double addsteps = Convert.ToDouble(zahl);
                    stepcounter += addsteps;
                    double menge = menge_kalib * stepcounter / 100;
                    m_aktuell = menge;
                    m_a.Text = Convert.ToString(menge);
                    break;

                case 'f':

                    string farben = indata.Replace("f", "");
                    char seperator = ',';
                    Farbe = farben.Split(seperator);
                    if (Farbe.Length == 6)
                    {
                        int v = Convert.ToInt32(Farbe[0]);
                        int b = Convert.ToInt32(Farbe[1]);
                        int g = Convert.ToInt32(Farbe[2]);
                        int y = Convert.ToInt32(Farbe[3]);
                        int o = Convert.ToInt32(Farbe[4]);
                        int r = Convert.ToInt32(Farbe[5]);

                        chart1.Series["Violet"].Points.AddXY(Zeit1, v);
                        chart1.Series["Blau"].Points.AddXY(Zeit1, b);
                        chart1.Series["Gruen"].Points.AddXY(Zeit1, g);
                        chart1.Series["Gelb"].Points.AddXY(Zeit1, y);
                        chart1.Series["Orange"].Points.AddXY(Zeit1, o);
                        chart1.Series["Rot"].Points.AddXY(Zeit1, r);
                    }
                    break;
                case 'p':
                    if (titration)
                    {
                        string phasen = indata.Replace("p", "");
                        int p = Convert.ToInt32(phasen);
                        switch (p)
                        {
                            case 1:
                                Phasenlabel.Text = "Die Titration befindet sich in der Anfangsphase. " +
                                    "Hierbei werden zwischen den Farbmessungen vergleichsweise viele Schritte gemacht.";
                                break;
                            case 2:
                                Phasenlabel.Text = "Die Titration befindet sich in der zweiten Phase. " +
                                    "Hier werden zwischen den Farbmessungen weniger Schritte gemacht, " +
                                    "sodass die Messung genauer wird.";
                                break;
                            case 3:
                                Phasenlabel.Text = "Die Titration befindet sich in der Endphase. " +
                                    "Der Umschlag wurde erkannt und es wird nun gewartet und später " +
                                    "erneut gemessen, ob der Farbumschlag geblieben ist.";
                                break;
                            case 4:
                                Phasenlabel.Text = "Titration Abgeschlossen.";
                                titration = false;
                                durchlauf += 1;
                                if (durchlauf == 1)
                                {
                                    m_1.Text = Convert.ToString(m_aktuell);
                                }
                                else if (durchlauf == 2)
                                {
                                    m_2.Text = Convert.ToString(m_aktuell);
                                }
                                else if (durchlauf == 3)
                                {
                                    m_3.Text = Convert.ToString(m_aktuell);
                                }
                                else if (durchlauf == 4)
                                {
                                    m_4.Text = Convert.ToString(m_aktuell);
                                }
                                else if (durchlauf == 5)
                                {
                                    m_5.Text = Convert.ToString(m_aktuell);
                                }
                                serialPort1.Write("S");
                                timer1.Stop();
                                timer1.Enabled = false;
                                titration = false;
                                gestoppt = true;
                                resettet = false;
                                groupBox1.Enabled = true;
                                m_aktuell = 0;
                                m_a.Text = "m_aktuell";
                                stepcounter = 0;
                                break;
                            case 5:
                                Phasenlabel.Text = "Pausiert";
                                break;
                        }
                    }
                    break;
            }
        }
        // Timer zur Chart Darstellung der Lichtwerte
        private void timer1_Tick(object sender, EventArgs e)
        {
            Zeit1++;
        }
        // Befehl die Titration zu starten, wobei Durchläufe<5
        private void button6_Click(object sender, EventArgs e)
        {
            if (connected && !titration)
            {
                if (durchlauf <= 5)
                {

                    
                    titration = true;
                    resettet = false;

                    timer1.Enabled = true;
                    timer1.Start();

                    serialPort1.Write("T");

                    gestoppt = false;

                    groupBox1.Enabled = false;
                    
                }
                else
                {
                    Fehlermeldung.Text = "Maximale Anzahl an Durchläufen erreicht.";
                }
            }
        }
        // Stop Befehl
        private void button7_Click(object sender, EventArgs e)
        {
            serialPort1.Write("S");

            timer1.Stop();
            timer1.Enabled = false;

            titration = false;
            gestoppt = true;

            groupBox1.Enabled = true;
            
        }
        // Reset Befehl
        private void button8_Click(object sender, EventArgs e)
        {
            if (gestoppt)
            {
                serialPort1.Write("R");

                chart1.Series["Violet"].Points.Clear();
                chart1.Series["Blau"].Points.Clear();
                chart1.Series["Gruen"].Points.Clear();
                chart1.Series["Gelb"].Points.Clear();
                chart1.Series["Orange"].Points.Clear();
                chart1.Series["Rot"].Points.Clear();

                titration = false;
                resettet = true;

                groupBox1.Enabled = true;
            }
                else
                {
                    Fehlermeldung.Text = "Pausiere zuerst die Titration mithilfe des STOP Buttons.";
                }
        }
        // Blendet Fehlermeldung bzgl. Waage aus, sobald Checkbox aktiviert wird
        private void tariert_CheckedChanged(object sender, EventArgs e)
        {
            if (tariert.Checked && Fehlermeldung.Text == "Checke, ob Waage tariert ist")
            {
                Fehlermeldung.Text = "(Meldungen)";
            }
        }
        // Ändert den Titrationsmodus von Färbungs- zu Trübungstitration
        private void Switch_Click(object sender, EventArgs e)
        {
            if (connected)
            {
                serialPort1.WriteLine("s");
                if (Switch.BackColor == Color.Fuchsia) 
                {
                    Switch.BackColor = Color.Bisque;
                }
                else
                {
                    Switch.BackColor = Color.Fuchsia;
                }
            }
        }
    }
}
