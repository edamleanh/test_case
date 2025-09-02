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

test('User can log in with valid credentials', async t => {

    await t
        .typeText(usernameInput, 'admin')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .pressKey('enter')
        .click(logoImg)
        .click(firstPostLink)
        .click(aceEditor)
        .typeText(aceTextArea, 'Test comment no preview', { replace: true })
        .click(postButton);
});

