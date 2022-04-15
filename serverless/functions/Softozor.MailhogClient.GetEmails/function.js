'use strict'

const createError = require('http-errors')
const mailhog = require('./common-mailhog/settings').function

exports.function = async input => {
  validateInput(input)

  const start = 'start' in input ? input.start : 0
  const limit = 'limit' in input ? input.limit : 50

  return await doGetMessages(start, limit)
}

const doGetMessages = async (start, limit) => {
  const result = await mailhog.messages(start, limit)

  if(result.items == undefined) {
    throw new createError.BadRequest('no email items')
  }

  result.items = result.items.map(item => {
    return {
      attachments: item.attachments,
      body: item.html,
      bcc: item.bcc,
      cc: item.cc,
      date: item.date,
      from: item.from,
      id: item.ID,
      replyTo: item.replyTo,
      subject: item.subject,
      to: item.Raw.To
    }
  })
  console.log(`Getting <${limit}> messages starting from <${start}>: `, result)
  return result
}

const validateInput = input => {
  checkArgIsPositive(input, 'start')
  checkArgIsPositive(input, 'limit')
}

const checkArgIsPositive = (input, propName) => {
  if (propName in input && input[propName] < 0) {
    throw new createError.BadRequest(`argument "${propName}" cannot be negative`)
  }
}
