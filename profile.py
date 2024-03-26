"""This is a trivial example of a gitrepo-based profile; The profile source code and other software, documentation, etc. are stored in in a publicly accessible GIT repository (say, github.com). When you instantiate this profile, the repository is cloned to all of the nodes in your experiment, to `/local/repository`. 

This particular profile is a simple example of using a single raw PC. It can be instantiated on any cluster; the node will boot the default operating system, which is typically a recent version of Ubuntu.

Instructions:
Wait for the profile instance to start, then click on the node in the topology and choose the `shell` menu item. 
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()
 
# Add a raw PC to the request.
node1 = request.RawPC("node1_rawPC")
node1.hardware_type = "m400"
node1.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD"

node2 = request.RawPC("node2_rawPC_withDocker")
node2.hardware_type = "m400"
node2.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD"

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
