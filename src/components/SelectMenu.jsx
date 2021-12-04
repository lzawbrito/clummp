
export default function SelectMenu(props) {
    function makeOption(op) {
        return <option value={op}>{op}</option>
    }

    const options = props.options.map(makeOption)
    return <>
    <label>{props.text}: </label>
    <select
        onChange={(e) => props.change(e.target.value)}>
        {options}
    </select>
    </>
}