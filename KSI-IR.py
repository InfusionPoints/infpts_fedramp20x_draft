    # KSI-IR.2: DynamoDB Point In time aws config check
    sec_response = dlm.get_lifecycle_policies()

    for acct in ACCOUNT_LIST:
        session=assume_role(acct, ROLE_NAME)
        dlm=session.client('dlm')
        response = dlm.get_lifecycle_policies()
        policies=response['Policies']
        all_accounts_policies.append({
            'account_id'  : acct,
            'policies' : policies
        })
        
    print(all_accounts_policies[2])
    # Examine the returned policies
    paginator = config.get_paginator('select_aggregate_resource_config')
    page_iterator = paginator.paginate(
    ConfigurationAggregatorName='organization-aggregator',
    Expression="""
        SELECT
          arn,
          supplementaryConfiguration.ContinuousBackupsDescription.continuousBackupsStatus,
          supplementaryConfiguration.ContinuousBackupsDescription.pointInTimeRecoveryDescription.pointInTimeRecoveryStatus
        WHERE
          resourceType = 'AWS::DynamoDB::Table'
    """
    )

    for page in page_iterator:
        for raw in page['Results']:
            snapshot = json.loads(raw)
            # drill down into the nested structure
            cb = snapshot.get('supplementaryConfiguration', {}) \
                        .get('ContinuousBackupsDescription', {}) \
                        .get('pointInTimeRecoveryDescription', {})
            # extract only the status
            status = cb.get('pointInTimeRecoveryStatus')
            # build the trimmed dict
            trimmed = {
                'pointInTimeRecoveryStatus': status,
                'arn': snapshot.get('arn')
            }
            total_trim.append(trimmed)
            

   ...
