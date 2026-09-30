// Recipe: Session-aware backend pool for an LLM (AI Gateway)
//
// Scenario:   Keep all requests for the same conversation/session pinned
//             to the same backend deployment, useful for providers that
//             cache conversation state server-side.
// Use when:   The model backend benefits from (or requires) sticky
//             sessions rather than pure load balancing.
// Requires:   Same as 11_backend_load_balancing_round_robin.bicep; a
//             session identifier available in the request (header or
//             claim) to key on.

resource backendPool 'Microsoft.ApiManagement/service/backends@2023-09-01-preview' = {
  name: '${apimServiceName}/openai-pool-session-aware'
  properties: {
    type: 'Pool'
    pool: {
      services: [
        { id: '/backends/openai-a' }
        { id: '/backends/openai-b' }
      ]
    }
  }
}

// The session key itself is supplied via policy, e.g.:
//   <set-backend-service backend-id="openai-pool-session-aware"
//       session-key="@(context.Request.Headers.GetValueOrDefault("x-session-id",""))" />
