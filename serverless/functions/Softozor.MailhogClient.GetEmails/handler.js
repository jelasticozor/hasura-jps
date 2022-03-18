'use strict'

const bodyParser = require('body-parser')
const getMessages = require('./getMessages').function

module.exports = ({ app }, wrap) => {
  app.use(bodyParser.json())
  app.post('/', wrap(getMessages))
}
