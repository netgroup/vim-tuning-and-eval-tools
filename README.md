Vim-tuning-and-eval-tools
================================

Tools for performance evaluation and tuning of Virtual Infrastructure Managers for (Micro) Virtual Network Functions

License
=============

This sofware is licensed under the Apache License, Version 2.0.

Information can be found here:
 [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

Structure
=============

The repository is organized in this way:
- **NOMAD.patch** contains our patch which adds the initial support for XEN hypervisor and some utility scripts;
- **NOMAD_tuned.patch** contains our patch which tunes the support for XEN hypervisor and contains some utility scripts;
- **driver_tuned_v1.py** contains our patch which adds the support for ClickOS in OpenStack;
- **nomad_utilities** folder contains scripts we used to generate Jobs, to analyze the packets and to generate the plots;
- **openstack_utilities** folder

Tips
==============

We report some suggestions useful to handle the code:
- **NOMAD_tuned.patch** depends on NOMAD.patch. 
- **NOMAD.patch** depends on commit 7f4140758ee0660e23303305a2634ef442a76114

Usage
==============

We report the usage of our scripts: