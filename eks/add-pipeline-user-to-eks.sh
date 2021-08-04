eksctl create iamidentitymapping \
    --cluster fargate-eks  \
    --arn arn:aws:iam::415428590389:user/user-pipeline-1 \
    --group system:masters \
    --username cicd-runner