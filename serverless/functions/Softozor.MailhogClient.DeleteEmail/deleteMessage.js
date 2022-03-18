'use strict'

const createError = require('http-errors')

const mailhog = require('./settings').function

exports.function = async input => {
  validateInput(input)

  const response = await mailhog.deleteMessage(input.id)

  if (response.statusCode === 200) {
    console.log(`Message <${input.id}> deleted.`)
    return {
      id: input.id
    }
  }

  console.error('Client request failed: ', response.statusCode, response.statusMessage)
  throw new createError.BadRequest(`Unable to delete message with id ${input.id}`)
}

const validateInput = input => {
  if (!('id' in input && input.id !== '')) {
    throw new createError.BadRequest('id missing from input')
  }
}
