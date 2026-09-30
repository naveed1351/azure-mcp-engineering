// Recipe: Priority-based backend pool preferring a PTU deployment
// (AI Gateway)
//
// Scenario:   Always route to a Provisioned Throughput Unit (PTU)
//             deployment first (guaranteed, prepaid capacity); only fall
//             back to a pay-as-you-go deployment when the PTU backend is
//             saturated or unhealthy.
// Use when:   You've purchased PTUs and want to maximize their
//             utilization before paying per-token elsewhere.
// Requires:   Same as 11_backend_load_balancing_round_robin.bicep, plus a
//             PTU deployment.

resource backendPool 'Microsoft.ApiManagement/service/backends@2023-09-01-preview' = {
  name: '${apimServiceName}/openai-pool-priority'
  properties: {
    type: 'Pool'
    pool: {
      services: [
        { id: '/backends/openai-ptu', priority: 1 }
        { id: '/backends/openai-payg', priority: 2 }
      ]
    }
  }
}
