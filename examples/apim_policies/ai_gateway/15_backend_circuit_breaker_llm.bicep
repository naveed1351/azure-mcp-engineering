// Recipe: Circuit breaker for an LLM backend (AI Gateway)
//
// Scenario:   Stop sending traffic to an LLM deployment that's returning
//             errors or throttling responses, honoring the backend's own
//             Retry-After header for recovery timing.
// Use when:   You want automatic, self-healing failover instead of a
//             blind retry loop (compare with
//             plain/12_retry_backend_call.xml, which is the wrong tool
//             for an already-overloaded LLM backend).
// Requires:   AI Gateway-capable API Management tier.

resource openaiBackend 'Microsoft.ApiManagement/service/backends@2023-09-01-preview' = {
  name: '${apimServiceName}/openai-payg'
  properties: {
    url: 'https://my-openai-resource.openai.azure.com'
    protocol: 'http'
    circuitBreaker: {
      rules: [
        {
          name: 'openaiBreakerRule'
          failureCondition: {
            count: 3
            interval: 'PT1M'
            statusCodeRanges: [ { min: 429, max: 429 }, { min: 500, max: 599 } ]
          }
          tripDuration: 'PT1M'
          acceptRetryAfter: true
        }
      ]
    }
  }
}
