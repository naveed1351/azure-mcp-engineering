// Recipe: Round-robin load-balanced backend pool for an LLM (AI Gateway)
//
// Scenario:   Spread chat-completion traffic evenly across two identical
//             Azure OpenAI deployments (for example, in two regions).
// Use when:   Both deployments have equivalent capacity/cost and you just
//             want to spread load and add redundancy.
// Requires:   AI Gateway-capable API Management tier; two backend
//             deployments with the same model/API surface.
// Decision:   For unequal-capacity deployments (a PTU deployment plus a
//             pay-as-you-go fallback), prefer
//             13_backend_load_balancing_priority_ptu.bicep instead.

resource backendPool 'Microsoft.ApiManagement/service/backends@2023-09-01-preview' = {
  name: '${apimServiceName}/openai-pool'
  properties: {
    type: 'Pool'
    pool: {
      services: [
        { id: '/backends/openai-eastus' }
        { id: '/backends/openai-westus' }
      ]
    }
  }
}
