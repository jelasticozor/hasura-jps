'use strict'

const bodyParser = require('body-parser')
const deleteMessage = require('./deleteMessage').function

module.exports = ({ app }, wrap) => {
  app.use(bodyParser.json())
  app.post('/', wrap(deleteMessage))
}
