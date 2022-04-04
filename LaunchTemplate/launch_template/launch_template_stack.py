from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as IAM
)
from constructs import Construct


class LaunchTemplateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs, tags={"cost-center": "8998",
                                                              "department": "Information-technology",
                                                              "workload-name": "rms-webserver-prod"})

        vpcName = self.node.try_get_context("vpcInput")
        VPC = ec2.Vpc.from_lookup(
            self,
            "VPCid",
            vpc_name=vpcName["vpcName"],
        )

        securityGroupInput = self.node.try_get_context("securityGroupInput")
        SecurityGroup = ec2.SecurityGroup(
            self,
            "SecurityGroupID",
            security_group_name=securityGroupInput["securityGroupName"],
            vpc=VPC
        )

        SecurityGroup.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(securityGroupInput["port1"])
        )
        SecurityGroup.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(securityGroupInput["port2"])
        )
        SecurityGroup.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(securityGroupInput["port3"])
        )

        iamInput = self.node.try_get_context("iamInput")
        IAMRole = IAM.Role.from_role_arn(
            self,
            "FromRoleARNId",
            role_arn=iamInput["roleARN"],
            mutable=iamInput["mutable"]
        )

        launchTemplateInput = self.node.try_get_context("launchTemplateInput")
        instanceInput = self.node.try_get_context("instanceInput")
        launchTemplate = ec2.LaunchTemplate(self,
                                            "LaunchTemplateId",
                                            machine_image=ec2.AmazonLinuxImage(),
                                            security_group=SecurityGroup,
                                            instance_type=ec2.InstanceType.of(
                                                ec2.InstanceClass[instanceInput["instanceClass"]],
                                                ec2.InstanceSize[instanceInput["instanceSize"]]),
                                            key_name=instanceInput["keyName"],
                                            launch_template_name=launchTemplateInput["launchTemplateName"],
                                            role=IAMRole,
                                            )
