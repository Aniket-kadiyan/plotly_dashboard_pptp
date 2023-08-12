Instructions:

      pre req:
            Ensure that the system has python installed.



      setup:

            open a commandpropmt/powershell/terminal at the location of requirements.txt
            run command:
                  pip install requirements.txt
            open dbcon.py and edit the name of the database, login crerdentials, sql server, tablenames, etc.

      to run the program on a deployment server use command:
            waitress-serve --host <host ip> --port <port address> pagetest:application
  
