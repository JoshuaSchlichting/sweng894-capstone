# This is required for the pipeline runner to be able to work with eksctl
# https://aws.amazon.com/blogs/containers/amazon-eks-cluster-automation-with-gitlab-ci-cd/
eksctl create iamidentitymapping \
    --cluster fargate-eks  \
    --arn arn:aws:iam::415428590389:user/user-pipeline-1 \
    --group system:masters \
    --username cicd-runner