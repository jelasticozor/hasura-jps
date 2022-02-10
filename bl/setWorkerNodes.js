function checkJelasticResponse(response, errorMsg) {
  if (!response || response.result !== 0) {
    throw errorMsg + ': ' + response
  }
}

function getNodesInfo(envName) {
  const resp = jelastic.environment.control.GetEnvInfo(envName, session)
  checkJelasticResponse(
    resp,
    "Cannot get environment info of environment <" +
      envName +
      ">, session <" +
      session +
      ">"
  )
  return resp.nodes
}

function getWorkerNodeServers(envName, serverPort) {
  var result = []
  const nodes = getNodesInfo(envName)
  for (var i = 0; i < nodes.length; ++i) {
    var node = nodes[i]
    if (node.nodeGroup == 'cp') {
      result.push('server ' + node.intIP + ':' + serverPort + '; ')
    }
  }
  return result.toString()
}

function replaceInBody(envName, path, pattern, replacement) {
  const resp = jelastic.environment.file.ReplaceInBody(
    envName,
    session,
    path,
    pattern,
    replacement,
    '', // nth
    '', // nodeType
    'bl' // nodeGroup
  )
  checkJelasticResponse(
    resp,
    'Replacing pattern <' +
      pattern +
      '> with <' +
      replacement +
      '> in file <' +
      path +
      '> failed!'
  )
}

function setWorkerNodes (envName, filename, placeholder, serverPort) {
  const workerNodes = getWorkerNodeServers(envName, serverPort)
  replaceInBody(envName, filename, placeholder, workerNodes)
}

return setWorkerNodes(getParam('TARGET_APPID'), getParam('filename'), getParam('workerNodesPlaceholder'))
