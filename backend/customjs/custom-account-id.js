const AWS = require('aws-sdk');


module.exports.getAccountId = async (context) => {
    return context.providers.aws.getAccountId();
};
