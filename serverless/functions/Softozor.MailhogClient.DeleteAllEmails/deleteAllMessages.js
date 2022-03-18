'use strict'

const createError = require('http-errors')

const mailhog = require('./settings').function

exports.function = async _ => {
  const messages = await mailhog.messages()
  const response = await mailhog.deleteAll()

  if (response.statusCode === 200) {
    console.log(`Deleted <${messages.total}> messages.`)
    return {
      deleted: messages.total
    }
  }

  console.error('Client request failed: ', response.statusCode, response.statusMessage)
  throw new createError.BadRequest('Unable to delete all messages')
}
