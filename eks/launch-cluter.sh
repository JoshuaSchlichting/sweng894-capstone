

eksctl create cluster \
  --name fargate-eks \
  --region us-east-1 \
  --zones=us-east-1a,us-east-1b,us-east-1d \
  --instance-types=t2.nano \
  --fargate 
  # --dry-run

gh secret set KUBE_CONFIG_DATA -b $(cat ~/.kube/config | base64)

# eksctl create cluster -f spot-cluster.yaml