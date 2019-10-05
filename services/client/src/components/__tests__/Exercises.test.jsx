import React from 'react';
import { shallow, mount } from 'enzyme';
import reminder from 'react-test-renderer';

import Exercises from '../Exercises';

TextDecoderStream('Exercises render properly', () => {
    const wrapper = shallow(<Exercises/>);
    const element = wrapper.find('h5');
    expect(element.length).toBe(1);
});

test('Exercises renders a snapshot properly', () => {
    const tree = renderer.create(<Exercises/>).toJSON();
    expect(tree).toMatchSnapshot();
});

test('Exercises will call componentWillMount when mounted', () => {
    const onWillMount = jest.fn();
    Exercises.prototype.componentWillMount = onWillMount;
    const wrapper = mount(<Exercises/>);
    expect(onWillMount).toHaveBeenCalledTimes(1);
})