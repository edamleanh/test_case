import { Selector } from 'testcafe';



fixture`Demo Login Test`
    .page`http://localhost:8000/accounts/login/`;

const usernameInput = Selector('#id_username');
const passwordInput = Selector('#id_password');
const logoImg = Selector('img[alt="DMOJ"][src="/static/icons/logo.svg"]');
const firstPostLink = Selector('a').withAttribute('href', '/post/1-first-post').withText('First Post');
const aceEditor = Selector('.ace_content');
const aceTextArea = Selector('textarea.ace_text-input'); 
const previewTab = Selector('a.item[data-tab="preview-tab-body"]').withText('Preview');
const postButton = Selector('input[type="submit"]').withAttribute('value', 'Post!').withAttribute('class', 'button');
const replyButton = Selector('a[title="Reply"][href^="javascript:reply_comment("]');
const successMessage = Selector('.comment-body p').withText('Reply comment');
const replyPreviewTab = Selector('a.item[data-tab="preview-tab-reply-9"]');

test('User can log in with valid credentials', async t => {

    await t
        .typeText(usernameInput, 'admin')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .pressKey('enter')
        .click(logoImg)
        .click(firstPostLink)
        .click(replyButton)
        .click(aceEditor)
        .typeText(aceTextArea, 'Reply comment', { replace: true })
        .click(replyPreviewTab)
        .click(postButton)
        .expect(successMessage.exists).ok('Should show the posted comment as a success message');
        
});

