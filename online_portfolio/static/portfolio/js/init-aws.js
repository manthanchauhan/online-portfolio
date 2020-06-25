var albumBucketName = "online-portfolio123";
var folder = "media";
var bucketRegion = "ap-south-1";
var IdentityPoolId = "ap-south-1:bea03113-7b8c-4f93-b2a9-8c2fb42e3115";

AWS.config.update({
  region: bucketRegion,
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: IdentityPoolId
  })
});

var s3 = new AWS.S3({
  apiVersion: "2006-03-01",
  params: { Bucket: albumBucketName + "/" + folder }
});
