#!/usr/bin/env python3
import os

import aws_cdk as cdk

from launch_template.launch_template_stack import LaunchTemplateStack


app = cdk.App()
env_ME = cdk.Environment(account="620228650709", region="me-south-1")
LaunchTemplateStack(app, "LaunchTemplateStack", env=env_ME)

app.synth()
