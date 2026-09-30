// Recipe: Register the embeddings backend used by semantic-cache policies
// (AI Gateway)
//
// Scenario:   llm-semantic-cache-lookup and azure-openai-semantic-cache-lookup
//             both need an `embeddings-backend-id` that resolves to a real
//             embeddings deployment (for example, text-embedding-3-small).
// Use when:   Setting up semantic caching for the first time -- this backend
//             resource is a one-time prerequisite referenced by
//             06/07 in this folder.
// Requires:   An Azure OpenAI (or other embeddings-capable) deployment;
//             the API Management instance's system-assigned managed
//             identity granted the "Cognitive Services OpenAI User" role
//             on that deployment.
// Decision:   This is infrastructure, not a policy -- create it once per
//             embeddings deployment, then reference its name from any
//             semantic-cache policy.

param apimServiceName string
param embeddingsEndpoint string // e.g. https://my-aoai.openai.azure.com

resource embeddingsBackend 'Microsoft.ApiManagement/service/backends@2023-09-01-preview' = {
  name: '${apimServiceName}/embeddings-backend'
  properties: {
    url: embeddingsEndpoint
    protocol: 'http'
    credentials: {
      // "system-assigned" managed identity auth, matching
      // embeddings-backend-auth="system-assigned" in the policy.
    }
  }
}
