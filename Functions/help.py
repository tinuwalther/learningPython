def usage():
  import os, sys, getopt
  '''Show a detailed help like in powershell'''
  print(f"\nNAME")
  print(f"    {os.path.basename(str(sys.argv[0]))}\n\n")

  print("SYNOPSIS")
  print(f"    Send a message to the listener\n\n")

  print("SYNTAX")
  print(f"    python3 {str(sys.argv[0])} -l <listener> -m <message>\n\n")

  print("DESCRIPTION")
  print(f"    Send a message to the listener, the listener run a command based on the message\n\n")

  print("PARAMETERS")
  print(f"    -l listener name or ip address\n\n")

  print("PARAMETERS")
  print(f"    -m keyword of the message to send: srf, wetter or covid are active\n\n")

  print(f"    -------------------------- EXAMPLE 1 --------------------------\n")
  print(f"    python3 {str(sys.argv[0])} -l pyhost1 -m wetter\n\n")

  print(f"    -------------------------- EXAMPLE 2 --------------------------\n")
  print(f"    python3 {str(sys.argv[0])} -l pyhost1 -m srf\n\n")

  print(f"    -------------------------- EXAMPLE 3 --------------------------\n")
  print(f"    python3 {str(sys.argv[0])} -l pyhost1 -m covid\n\n")