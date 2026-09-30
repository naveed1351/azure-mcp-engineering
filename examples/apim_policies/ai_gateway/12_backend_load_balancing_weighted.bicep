// Recipe: Weighted load-balanced backend pool for an LLM (AI Gateway)
//
// Scenario:   Send roughly 80% of traffic to a primary deployment and 20%
//             to a secondary one -- useful for gradually shifting traffic
//             to a new region or model version.
// Use when:   Deployments aren't equal, but you still want the gateway to
//             split traffic automatically rather than routing by policy
//             logic.
// Requires:   Same as 11_backend_load_balancing_round_robin.bicep.

resource backendPool 'Microsoft.ApiManagement/service/backends@2023-09-01-preview' = {
  name: '${apimServiceName}/openai-pool-weighted'
  properties: {
    type: 'Pool'
    pool: {
      services: [
        { id: '/backends/openai-primary', weight: 80 }
        { id: '/backends/openai-secondary', weight: 20 }
      ]
    }
  }
}
