const mongoose = require('mongoose');

const querySchema = new mongoose.Schema({
    user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    urls : [String],
    condition : String,
    llmresponse : String,
    prescription: [String],
    suggestions: [String],
    docters: [String],

});

module.exports = mongoose.models.Post || mongoose.model('Query', querySchema);
